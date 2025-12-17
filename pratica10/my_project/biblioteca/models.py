from django.db import models
class Autor(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nome

class Editora(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255, unique=True)
    

    def __str__(self):
        return self.nome

class Livro(models.Model):
    id = models.AutoField(primary_key=True)
    isbn = models.CharField(max_length=13, unique=True)
    autor = models.ForeignKey(
        Autor, 
        on_delete=models.CASCADE
    )
    titulo = models.CharField(max_length=500)
    publicacao = models.DateField()
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    estoque = models.IntegerField()
    editora = models.ForeignKey(Editora, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo