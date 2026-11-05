#!/usr/bin/env python3
"""Read-only exact alpha-template check. Requires Pillow; no 3D validation."""
import argparse
from collections import deque
import hashlib
import json
from pathlib import Path
import sys
from PIL import Image


def islands(alpha, width, height):
    """Count 4-connected regions at alpha >= 128; never infer panel names."""
    remaining = bytearray(value >= 128 for value in alpha)
    counts = []
    for start in range(len(remaining)):
        if not remaining[start]:
            continue
        remaining[start] = 0
        queue = deque([start])
        area = 0
        while queue:
            i = queue.popleft()
            area += 1
            x, y = i % width, i // width
            for j in (i - 1 if x else -1,
                      i + 1 if x + 1 < width else -1,
                      i - width if y else -1,
                      i + width if y + 1 < height else -1):
                if j >= 0 and remaining[j]:
                    remaining[j] = 0
                    queue.append(j)
        counts.append(area)
    return sorted(counts, reverse=True)


def check(template, candidate):
    report = {'passed': False,
              'scope': 'Exact 2D alpha silhouettes only; artwork and on-car orientation unverified',
              'errors': []}
    try:
        for key, path in [('template', template), ('candidate', candidate)]:
            report[key + '_sha256'] = hashlib.sha256(Path(path).read_bytes()).hexdigest()
        with Image.open(template) as reference, Image.open(candidate) as output:
            reference.load()
            output.load()
            report['template_dimensions'] = list(reference.size)
            report['candidate_dimensions'] = list(output.size)
            if reference.size != output.size:
                raise ValueError('dimension mismatch; do not resize inside the checker')
            if getattr(reference, 'n_frames', 1) != 1 or getattr(output, 'n_frames', 1) != 1:
                raise ValueError('animated images are not supported')
            expected = reference.convert('RGBA').getchannel('A').tobytes()
            actual = output.convert('RGBA').getchannel('A').tobytes()
            if min(expected) == max(expected):
                raise ValueError('template has no usable alpha silhouette; an explicit mask is required')
            report['alpha_changed_pixels'] = sum(a != b for a, b in zip(expected, actual))
            report['spill_pixels'] = sum(a == 0 and b > 0 for a, b in zip(expected, actual))
            report['missing_opaque_pixels'] = sum(a == 255 and b < 255 for a, b in zip(expected, actual))
            report['max_alpha_difference'] = max(abs(a - b) for a, b in zip(expected, actual))
            report['reference_island_areas_at_alpha_128'] = islands(expected, *reference.size)
            if report['alpha_changed_pixels']:
                report['errors'].append('candidate alpha does not exactly match the template')
            report['passed'] = not report['errors']
    except Exception as exc:
        report['errors'].append(str(exc))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--template', required=True, type=Path)
    parser.add_argument('--candidate', required=True, type=Path)
    args = parser.parse_args()
    report = check(args.template, args.candidate)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
