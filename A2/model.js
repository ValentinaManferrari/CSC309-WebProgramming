class Item {
	constructor(name, price, quantity) {
		this.name = name;
		this.price = price;
		this.quantity = quantity;
		this.total = price * quantity;
	}
}