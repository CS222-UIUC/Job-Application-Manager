import json
from pathlib import Path

from django.core.management.base import BaseCommand

from leetcode.models import LeetCodeProblem


class Command(BaseCommand):
    help = "Load LeetCode problems from local JSON file"

    def handle(self, *args, **options):
        data_path = Path(__file__).resolve().parents[3] / "leetcode_first_3758.json"

        with open(data_path, "r", encoding="utf-8") as f:
            problems = json.load(f)

        total = len(problems)
        self.stdout.write(f"Found {total} problems in JSON")

        created, updated = 0, 0

        for idx, p in enumerate(problems):
            problem_id = total - idx  # the json file is in reverse order

            obj, was_created = LeetCodeProblem.objects.update_or_create(
                problem_id=problem_id,
                defaults={
                    "title": p["title"].strip(),
                    "difficulty": p["difficulty"],
                    "tags": p.get("topics", []),
                    "url": p.get("link", ""),
                },
            )

            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(f"Loaded {total} problems ({created} created, {updated} updated)")
        )
