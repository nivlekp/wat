import importlib
import sys

from SegmentHandler import SegmentHandler

import abjad


class SegmentIllustrator(SegmentHandler):
    """
    Segment Illustrator.
    """

    def __call__(self):
        for seg in self._segments:
            segments_path = self._segments_dir / seg
            assert self._is_segment_directory(segments_path)
            definition = importlib.import_module("utsu.segments." + seg + ".definition")
            lilypond_file = definition.segment_maker.run()
            with open(str(segments_path / "illustration.ly"), "w") as file_pointer:
                file_pointer.write(abjad.lilypond(lilypond_file))
            self._write_segments_to_build(lilypond_file, seg)

    def _write_segments_to_build(self, lilypond_file, seg):
        # TODO: make this into a zsh script
        score_path = self._builds_dir / "score"
        # formatted_blocks = lilypond_file.score_block
        # print(abjad.lilypond(formatted_blocks))
        with open(str(score_path / (seg + ".ly")), "w") as file_pointer:
            file_pointer.write(abjad.lilypond(lilypond_file.items[0]))
        # TODO: change this method to a better one
        with open(str(score_path / (seg + ".ly")), "r") as file_pointer:
            block = file_pointer.read().splitlines(True)
        # with open(str(score_path / (seg + ".ly")), "w") as file_pointer:
        # file_pointer.writelines(block[1:-1])


if __name__ == "__main__":
    illustrator = SegmentIllustrator(sys.argv[1:])
    illustrator()
