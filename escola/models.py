from django.db import models

# Create your models here.
class BaseModel(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Aluno(BaseModel):
    nome = models.CharField(max_length=100, blank=False, null=False)
    rg = models.CharField(max_length=9, blank=False, null=False)
    cpf = models.CharField(max_length=11, blank=False, null=False)
    data_nascimento = models.DateField(blank=False, null=False)

    def save(self, *args, **kwargs):
        self.nome = self.nome.title()
        return super(Aluno, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.nome


class Curso(BaseModel):
    NIVEL = (("B", "Básico"), ("I", "Intermediário"), ("A", "Avançado"))

    codigo_curso = models.CharField(max_length=10, unique=True, blank=False, null=False)
    descricao = models.CharField(max_length=100)
    nivel = models.CharField(
        max_length=1, choices=NIVEL, blank=False, null=False, default="B"
    )

    def save(self, *args, **kwargs):
        self.descricao = self.descricao.capitalize()
        return super(Curso, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.descricao


class Matricula(BaseModel):
    PERIODO = (("M", "Matutino"), ("V", "Vespertino"), ("N", "Noturno"))

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    periodo = models.CharField(max_length=1, choices=PERIODO, blank=False, null=False)

    def __str__(self) -> str:
        return f"{self.aluno.nome} - {self.curso.codigo_curso} / {self.periodo.get_periodo_display()}"
