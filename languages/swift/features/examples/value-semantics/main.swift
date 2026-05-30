struct CartItem {
    let name: String
    var quantity: Int
}

struct Cart {
    private(set) var items: [CartItem]

    var totalQuantity: Int {
        items.reduce(0) { total, item in total + item.quantity }
    }

    mutating func add(_ name: String, quantity: Int) {
        items.append(CartItem(name: name, quantity: quantity))
    }
}

final class ReferenceCounter {
    private(set) var value = 0

    func increment() {
        value += 1
    }
}

let original = Cart(items: [
    CartItem(name: "Guide Book", quantity: 1),
    CartItem(name: "Notebook", quantity: 2)
])

var draft = original
draft.add("Pencil", quantity: 3)

print("Original cart quantity:", original.totalQuantity)
print("Draft cart quantity:", draft.totalQuantity)

let sharedCounter = ReferenceCounter()
let anotherHandle = sharedCounter

sharedCounter.increment()
anotherHandle.increment()

print("Shared class counter:", sharedCounter.value)
