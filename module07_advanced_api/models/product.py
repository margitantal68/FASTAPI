class Product:
    def __init__(self, id: int, name: str, price: float, description: str = None):
        self.id = id
        self.name = name
        self.price = price
        self.description = description

    def __repr__(self):
        return f"Product(id={self.id}, name={self.name}, price={self.price}, description={self.description})"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "description": self.description
        }
    
items = [
    Product(id=1, name="Book with title: Egri csillagok", price=50.0, description="A historical novel by Géza Gárdonyi."),
    Product(id=2, name="Book with title: A Pál utcai fiúk", price=45.0, description="A novel by Ferenc Molnár about a group of boys"),
    Product(id=3, name="Book with title: A kis herceg", price=60.0, description="A novel by Antoine de Saint-Exupéry about a young prince"),
]

def fill_items_list():
    for i in range(4, 51):
        items.append(Product(id=i, name=f"Book with title: Book {i}", price=20.0 + i, description=f"Description for book {i}"))
    for i in range(51, 101):
        items.append(Product(id=i, name=f"Fruit: Fruit {i}", price=1.0 + i, description=f"Description for fruit {i}"))

