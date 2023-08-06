""" DEPRECATION WARNING:
This file is currently unused by FluentDNA.  The original purpose was to show
a variety of MSA pulled from RepeatMasker annotations across the genome.
The intent was to visualize the diversity and abundance at each site.
All the reusable functionality of TransposonLayout has been moved to MultipleAlignmentLayout.
A fairly small script could process the repeatMasker annotation file into a folder of fasta MSA
that could be visualized with MultipleAlignmentLayout.
The crucial values are the within repeat coordinates rep_end.  I found experimentally
that rooting the MSA on the last nucleotide of each line (not the start) gave the most
coherent MSA."""

from __future__ import print_function, division, absolute_import, \
    with_statement, generators, nested_scopes
import math
import traceback

from DNASkittleUtils.DDVUtils import editable_str
from collections import defaultdict
from datetime import datetime

from DNASkittleUtils.Contigs import Contig, read_contigs
from DNASkittleUtils.DDVUtils import rev_comp
from FluentDNA.RepeatAnnotations import read_repeatmasker_csv, max_consensus_width, blank_line_array
from FluentDNA.TileLayout import TileLayout
from FluentDNA import gap_char
from FluentDNA.FluentDNAUtils import copy_to_sources


class TransposonLayout(TileLayout):
    def __init__(self, **kwargs):
        # print("Warning: Transposon Layout is an experimental feature not currently supported.",
        #       file=sys.stderr)
        kwargs.update({'sort_contigs': True})  # important for mega row height handling
        super(TransposonLayout, self).__init__(**kwargs)
        self.repeat_entries = None
        self.current_column_height = 20
        self.next_origin = [self.border_width, 30] # margin for titles, incremented each MSA



    def create_image_from_preprocessed_alignment(self, input_file_path, consensus_width, num_lines, output_folder, output_file_name):
        print("Warning: This feature is currently unsupported")
        self.initialize_image_by_sequence_dimensions(consensus_width, num_lines)  # sets self.layout
        self.read_contigs_and_calc_padding(input_file_path)
        super(TransposonLayout, self).draw_nucleotides()  # uses self.contigs and self.layout to draw
        self.output_image(output_folder, output_file_name, False)


    def process_all_repeats(self, ref_fasta, output_folder, output_file_name, repeat_annotation_filename, chromosomes=None):
        self.levels.origin = (self.levels.origin[0], self.levels.origin[1] + self.levels[5].padding)  # One full Row of padding for Title
        start_time = datetime.now()
        self.read_all_files(ref_fasta, repeat_annotation_filename, chromosomes)

        print("Read contigs :", datetime.now() - start_time)

        self.initialize_image_by_sequence_dimensions()
        print("Initialized Image:", datetime.now() - start_time, "\n")
        try:  # These try catch statements ensure we get at least some output.  These jobs can take hours
            self.draw_nucleotides()
            print("\nDrew Nucleotides:", datetime.now() - start_time)
        except Exception as e:
            print('Encountered exception while drawing nucleotides:', '\n')
            traceback.print_exc()
        self.output_image(output_folder, output_file_name, False)
        print("Output Image in:", datetime.now() - start_time)
        copy_to_sources(output_folder, ref_fasta)
        copy_to_sources(output_folder, repeat_annotation_filename)


    def max_dimensions(self, image_length):
        rough = int(math.ceil(math.sqrt(image_length * 3)))
        rough = min(62900, rough)  # hard cap at 4GB images created
        # Layout should never be more narrow than the widest single element
        min_width = max(rough, self.levels[2].thickness + (self.levels.origin[0] * 2))
        return min_width, rough + self.levels.origin[1]


    def initialize_image_by_sequence_dimensions(self, consensus_width=None, num_lines=None):
        if consensus_width is None:
            consensus_width = sum([x.rep_end for x in self.repeat_entries]) // len(self.repeat_entries)  # rough approximation of size
            num_lines = len(self.repeat_entries)
            print("Average Width", consensus_width, "Entries", num_lines)
            heights = self.repeat_entries_to_heights()
            self.set_column_height(heights)
        else:
            self.current_column_height = 1000

        self.image_length = consensus_width * num_lines
        self.prepare_image(self.image_length)
        print("Image is ", self.image.width, "x", self.image.height)


    def read_all_files(self, ref_fasta, repeat_annotation_filename, chromosomes=None):
        if repeat_annotation_filename is None:  # necessary for inheritance requirements
            raise NotImplementedError("TransposonLayout requires a repeat annotation to work")
        print('Getting all annotations in ', chromosomes)
        column = 'genoName'
        self.repeat_entries = read_repeatmasker_csv(repeat_annotation_filename, column, chromosomes)
        self.filter_simple_repeats(return_only_simple_repeats=False)
        self.repeat_entries.sort(key=lambda x: -len(x) + x.geno_start / 200000000)  # longest first, chromosome position breaks ties
        print("Found %s entries under %s" % ('{:,}'.format(len(self.repeat_entries)), str(chromosomes)))
        self.contigs = read_contigs(ref_fasta)


    def filter_simple_repeats(self, return_only_simple_repeats=False):
        # TODO: option to keep ONLY simple_repeats and delete everything else
        before = len(self.repeat_entries)
        if return_only_simple_repeats:
            self.repeat_entries = [x for x in self.repeat_entries if x.rep_class == 'Simple_repeat']  # remove 'simple'
        else:
            self.repeat_entries = [x for x in self.repeat_entries if x.rep_class != 'Simple_repeat']  # remove 'simple'
        difference = before - len(self.repeat_entries)
        print("Removed", difference, "repeats", "{:.1%}".format(difference / before), "of the data.")



    def draw_nucleotides(self, verbose=True):
        processed_contigs = self.create_repeat_fasta_contigs()
        print("Finished creating contigs")
        self.contigs = processed_contigs  # TODO: overwriting self.contigs isn't really great data management
        self.draw_nucleotides_in_variable_column_width()  # uses self.contigs and self.layout to draw


    def draw_nucleotides_in_variable_column_width(self):
        """Layout a whole set of different repeat types with different widths.  Column height is fixed,
        but column width varies constantly.  Wrapping to the next row is determined by hitting the
        edge of the allocated image."""
        for contig in self.contigs:
            assert contig.consensus_width, "You must set the consensus_width in order to use this layout"
            height = math.ceil(len(contig.seq) / contig.consensus_width)
            self.layout_based_on_repeat_size(contig.consensus_width, height, self.image.width)

            contig_progress = 0
            seq_length = len(contig.seq)
            line_width = contig.consensus_width
            for cx in range(0, seq_length, line_width):
                try:
                    x, y = self.position_on_screen(contig_progress)
                    if x + contig.consensus_width + 1 >= self.image.width:
                        self.fail_to_next_mega_row(contig)
                        break
                    if y + self.levels[1].modulo >= self.image.height:
                        print("Ran into bottom of image at", contig.name, x,y)
                        return contig  # can't fit anything more
                    if y == self.levels.origin[1]:  # first line in a column
                        self.draw_repeat_title(contig, x, y)

                    remaining = min(line_width, seq_length - cx)
                    contig_progress += remaining
                    for i in range(remaining):
                        nuc = contig.seq[cx + i]
                        # if nuc != gap_char:
                        self.draw_pixel(nuc, x + i, y)
                except IndexError as e:
                    print("(%i, %i)" % (x,y), "is off the canvas")
            print("Drew", contig.name, "ending at", self.position_on_screen(contig_progress))
        print('')


    def fail_to_next_mega_row(self, contig):
        print("Not enough room to draw", contig.name, "at", self.levels.origin)
        self.next_origin = [self.border_width,
                            self.next_origin[1] + len(contig.seq)//contig.consensus_width + 10]


    def create_repeat_fasta_contigs(self):
        processed_contigs = []
        rep_names = list({x.rep_name for x in self.repeat_entries})
        rep_names.sort()  # iterate through unique set in alphabetical order
        for rep_name in rep_names:
            contig = self.make_contig_from_repName(rep_name)
            lines_in_contig = len(contig.seq) // contig.consensus_width
            # minimum number of repeats based on aspect ratio 1:20
            if lines_in_contig > 10 and lines_in_contig > contig.consensus_width // 20:
                print("Collected repeats sequences for", contig)
                processed_contigs.append(contig)
        return processed_contigs


    def make_contig_from_repName(self, rep_name):
        annotations = [x for x in self.repeat_entries if x.rep_name == rep_name]
        consensus_width = max_consensus_width(annotations)
        ordered_lines = defaultdict(lambda: gap_char * consensus_width)
        for contig in self.contigs:
            for line_number, fragment in enumerate(annotations):
                if fragment.geno_name == contig.name:
                    line = grab_aligned_repeat(consensus_width, contig, fragment)
                    ordered_lines[line_number] = ''.join(line)
        processed_seq = ''.join([ordered_lines[i] for i in range(len(annotations))])
        contig_name = '__'.join([annotations[0].rep_name, annotations[0].rep_family, annotations[0].rep_class])
        c = Contig(contig_name, processed_seq, )
        c.consensus_width=consensus_width
        return c

    def draw_repeat_title(self, contig, x, y):
        chars_per_line = int(math.ceil(contig.consensus_width / 5.625))
        height = 30
        self.write_title(contig.name,
                         width=contig.consensus_width,
                         height=height - 5,
                         font_size=9,
                         title_lines=2,
                         title_width=chars_per_line,
                         upper_left=[x, y - height],
                         vertical_label=False,
                         canvas=self.image)

    def set_column_height(self, heights):
        try:
            from statistics import median
            average_line_count = int(median(heights))
        except ImportError:
            average_line_count = int(math.ceil(sum(heights) / len(heights)))
        self.current_column_height = min(max(heights), average_line_count * 2)
        print("Setting Column Height to %i based on Average line count per Block" % self.current_column_height)

    def repeat_entries_to_heights(self):
        rep_count = defaultdict(lambda: 0)
        for x in self.repeat_entries:
            rep_count[x.rep_name] += 1
        heights = sorted([val for val in rep_count.values()])
        return heights


def grab_aligned_repeat(consensus_width, contig, fragment):
    line = blank_line_array(consensus_width, gap_char, newline=False)
    nucleotides = fragment.genome_span().sample(contig.seq)
    if fragment.strand == '-':
        nucleotides = rev_comp(nucleotides)
    if fragment.rep_end - len(nucleotides) < 0:  # sequence I have sampled starts before the beginning of the frame
        nucleotides = nucleotides[len(nucleotides) - fragment.rep_end:]  # chop off the beginning
    line = line[:fragment.rep_end - len(nucleotides)] + editable_str(nucleotides) + line[fragment.rep_end:]
    assert len(line) == consensus_width, "%i, %i" % (len(line), consensus_width, )

    return line