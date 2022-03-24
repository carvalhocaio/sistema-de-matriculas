from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


from rest_framework import viewsets, generics, status
from rest_framework.response import Response

from escola.models import Aluno, Curso, Matricula
from escola.serializers import (
    AlunoSerializer,
    AlunoSerializerV2,
    CursoSerializer,
    MatriculaSerializer,
    ListaMatriculasAlunoSerializer,
    ListaAlunosMatriculadosSerializer,
)


class AlunosViewSet(viewsets.ModelViewSet):
    """Exibe todos os alunos"""

    queryset = Aluno.objects.all()

    def get_serializer_class(self):
        if self.request.version == "v2":
            return AlunoSerializerV2
        else:
            return AlunoSerializer


class CursosViewSet(viewsets.ModelViewSet):
    """Exibe todos os cursos"""

    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = Response(serializer.data, status=status.HTTP_201_CREATED)
            id = str(serializer.data[id])
            response["Location"] = request.build_absolute_uri() + id
            return response


class MatriculasViewSet(viewsets.ModelViewSet):
    """Lista todas as matrículas"""

    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer
    http_methods_names = ["get", "post", "put", "patch"]

    @method_decorator(cache_page(20))
    def dispatch(self, *args, **kwargs):
        return super(MatriculasViewSet, self).dispatch(*args, **kwargs)


class ListaMatriculasAluno(generics.ListAPIView):
    """Lista as matrículas de um aluno"""

    def get_queryset(self):
        queryset = Matricula.objects.filter(Aluno_id=self.kwargs["pk"])
        return queryset

    serializer_class = ListaMatriculasAlunoSerializer


class ListaAlunosMatriculados(generics.ListAPIView):
    """Lista alunos matricualdos em um curso"""

    def get_queryset(self):
        queryset = Matricula.objects.filter(curso_id=self.kwargs["pk"])
        return queryset

    serializer_class = ListaAlunosMatriculadosSerializer
