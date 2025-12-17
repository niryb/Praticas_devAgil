from rest_framework import serializers
from .models import Livro, Autor, Editora


class LivroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livro
        fields = ['id', 'isbn', 'autor', 'titulo', 'publicacao', 'preco', 'estoque', 'editora']
        read_only_fields = ['id']

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = ['id', 'nome']
        read_only_fields = ['id']

    def validate_nome(self, value):
        if value == '0':
            raise serializers.ValidationError(
                "Validação teste"
            )
        return value

class EditoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editora
        fields = ['id', 'nome']
        read_only_fields = ['id']