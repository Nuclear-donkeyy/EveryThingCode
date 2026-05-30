const rawOrders = [
  '{"id":"ord-1001","items":[{"sku":"tea","quantity":2},{"sku":"cup","quantity":1}],"priority":true}',
  '{"id":"ord-1002","items":[{"sku":"coffee","quantity":3}],"priority":false}',
  '{"id":1003,"items":[{"sku":"bad","quantity":"many"}]}',
];

function isPlainObject(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function isOrder(value) {
  return (
    isPlainObject(value) &&
    typeof value.id === "string" &&
    Array.isArray(value.items) &&
    value.items.every(
      (item) =>
        isPlainObject(item) &&
        typeof item.sku === "string" &&
        Number.isInteger(item.quantity) &&
        item.quantity > 0,
    ) &&
    (value.priority === undefined || typeof value.priority === "boolean")
  );
}

function parseOrder(json) {
  const value = JSON.parse(json);
  if (!isOrder(value)) {
    throw new TypeError(`Invalid order shape: ${json}`);
  }
  return value;
}

function summarizeOrder(order) {
  const totalItems = order.items.reduce((sum, item) => sum + item.quantity, 0);
  const priorityLabel = order.priority ? "priority" : "standard";
  return `${order.id}: ${totalItems} item(s), ${priorityLabel}`;
}

for (const rawOrder of rawOrders) {
  try {
    const order = parseOrder(rawOrder);
    console.log(summarizeOrder(order));
  } catch (error) {
    console.log(error.message);
  }
}
