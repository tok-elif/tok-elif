from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ProfileAutomationTests(unittest.TestCase):
    def test_snake_refreshes_on_main_push_and_every_six_hours(self):
        workflow = (ROOT / ".github/workflows/snake.yml").read_text()

        self.assertRegex(workflow, r'cron:\s*["\']\d+ \*/6 \* \* \*["\']')
        self.assertRegex(workflow, r"(?m)^\s{2}push:\s*$")
        self.assertRegex(workflow, r"(?m)^\s{6}- main\s*$")

    def test_streak_is_generated_locally_and_not_loaded_from_heroku(self):
        readme = (ROOT / "README.md").read_text()
        workflow_path = ROOT / ".github/workflows/streak-stats.yml"

        self.assertTrue(workflow_path.exists())
        self.assertIn('src="./profile/streak.svg"', readme)
        self.assertNotIn("github-readme-streak-stats.herokuapp.com", readme)

    def test_streak_refreshes_without_a_bot_commit_loop(self):
        workflow_path = ROOT / ".github/workflows/streak-stats.yml"

        self.assertTrue(workflow_path.exists())
        workflow = workflow_path.read_text()

        self.assertRegex(workflow, r'cron:\s*["\']\d+ \*/6 \* \* \*["\']')
        self.assertIn("workflow_dispatch:", workflow)
        self.assertRegex(workflow, r"(?m)^\s{2}push:\s*$")
        self.assertIn("paths-ignore:", workflow)
        self.assertIn('"profile/streak.svg"', workflow)
        self.assertIn("path: profile/streak.svg", workflow)
        self.assertIn("timezone=Europe/Istanbul", workflow)


if __name__ == "__main__":
    unittest.main()
