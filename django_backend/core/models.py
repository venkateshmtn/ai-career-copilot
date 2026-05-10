from django.db import models


class ResumeAnalysis(models.Model):
    resume_text = models.TextField()
    job_description = models.TextField()

    score = models.IntegerField()
    matched_skills = models.JSONField()
    missing_skills = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis {self.id} - Score {self.score}"