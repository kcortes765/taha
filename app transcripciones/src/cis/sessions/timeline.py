from __future__ import annotations

from cis.domain.models import Transcript


def build_timeline(transcripts: list[Transcript]) -> list[str]:
    seen_starts: set[float] = set()
    timeline: list[str] = []
    for transcript in transcripts:
        for segment in transcript.segments[:10]:
            if segment.start in seen_starts:
                continue
            seen_starts.add(segment.start)
            timeline.append(f"{segment.start:06.2f}-{segment.end:06.2f} {segment.text}")
    return timeline[:20]

