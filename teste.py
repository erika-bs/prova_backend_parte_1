from domain.category import Category
from shared.timeutil import iso_utc

print("Teste Category")

categoria = Category(name="Roupas femininas", description="vestuário feminino")
print("=======================================================================")
print("Serialização:")
d = categoria.to_dict()
print(f"Categoria após serialização: {d}")

categoria2 = Category.from_dict(d)
print(f"Reconstruído: {categoria2}")
print("=======================================================================")
print("Eventos iniciais:")

for e in categoria.events:
    print(type(e).__name__, "| aconteceu:", iso_utc(e.occurred_on))

print("=======================================================================")
categoria.update(name="Roupas masculinas", description="vestuário masculino")
print(f"Categoria após update: {categoria}")
categoria.deactivate()
categoria.activate()
print("=======================================================================")
print("Eventos após update/desativar/ativar:")

for e in categoria.events:
    print(f"{type(e).__name__} | aconteceu {iso_utc(e.occurred_on)}")