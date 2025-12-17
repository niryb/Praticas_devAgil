# biblioteca/management/commands/generate_books.py

import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from faker import Faker
from biblioteca.models import Autor, Editora, Livro

class Command(BaseCommand):
    help = 'Gera 100 registros de livros falsos no banco de dados.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Iniciando a geração de dados...'))
        
        fake = Faker('pt_BR')
        
        # --- 1. Garantir que Autores e Editoras existam ---
        
        # Busca existentes ou cria novos
        autores = list(Autor.objects.all())
        if not autores:
            self.stdout.write('Nenhum autor encontrado. Criando 10 autores...')
            for _ in range(10):
                autores.append(Autor.objects.create(nome=fake.name()))
        
        editoras = list(Editora.objects.all())
        if not editoras:
            self.stdout.write('Nenhuma editora encontrada. Criando 5 editoras...')
            for _ in range(5):
                editoras.append(Editora.objects.create(nome=fake.company()))

        # --- 2. Gerar 100 Livros ---
        livros_criados = []
        for _ in range(100):
            # Seleciona aleatoriamente dos que já existem ou acabamos de criar
            autor = random.choice(autores)
            editora = random.choice(editoras)
            
            # Gera dados falsos
            isbn = fake.isbn13(separator="")
            
            # Cuidado: Seu modelo limita o título a 20 caracteres!
            titulo = fake.catch_phrase()[:500] 
            
            publicacao = fake.date_between(start_date='-10y', end_date='today')
            preco = Decimal(fake.pydecimal(left_digits=4, right_digits=2, positive=True, min_value=10, max_value=200))
            estoque = fake.random_int(min=1, max=100)
            
            # Cria o livro
            try:
                livro = Livro.objects.create(
                    isbn=isbn,
                    autor=autor,
                    titulo=titulo,
                    publicacao=publicacao,
                    preco=preco,
                    estoque=estoque,
                    editora=editora
                )
                livros_criados.append(livro)
            except Exception as e:
                # Pode falhar se o ISBN (unique) ou Título (max_length) derem problema
                self.stdout.write(self.style.WARNING(f'Não foi possível criar livro. Erro: {e}'))

        self.stdout.write(self.style.SUCCESS(f'{len(livros_criados)} livros foram gerados com sucesso!'))