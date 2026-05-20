from django.db import models


class DimCompany(models.Model):
    symbol = models.CharField(primary_key=True, max_length=50, db_column='id')
    company_name = models.CharField(max_length=255, db_column='company_name')
    about_company = models.TextField(blank=True, null=True, db_column='about_company')
    website = models.URLField(blank=True, null=True, db_column='website')
    face_value = models.DecimalField(max_digits=10, decimal_places=2, db_column='face_value', null=True)

    class Meta:
        managed = False
        db_table = 'dim_company'

    def __str__(self):
        return f"{self.symbol} - {self.company_name}"

class FactMlScores(models.Model):
    company_id = models.CharField(primary_key=True, max_length=50)
    overall_score = models.IntegerField()
    health_label = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'fact_ml_scores'

    def __str__(self):
        return f"{self.company_id}: {self.overall_score}"


class FactCashFlow(models.Model):
    company_id = models.CharField(primary_key=True, max_length=50, db_column='company_id')
    fiscal_year = models.IntegerField(db_column='fiscal_year')
    operating_activity = models.DecimalField(max_digits=15, decimal_places=2)
    net_cash_flow = models.DecimalField(max_digits=15, decimal_places=2)
    free_cash_flow = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'fact_cash_flow'
        unique_together = (('company_id', 'fiscal_year'),)