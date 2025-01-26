const express = require('express');
const redis = require('redis');
const { promisify } = require('util');

// Create an Express app
const app = express();
const port = 1245;

// Connect to Redis
const client = redis.createClient();
const setAsync = promisify(client.set).bind(client);
const getAsync = promisify(client.get).bind(client);

// Product data
const listProducts = [
  { itemId: 1, itemName: "Suitcase 250", price: 50, initialAvailableQuantity: 4 },
  { itemId: 2, itemName: "Suitcase 450", price: 100, initialAvailableQuantity: 10 },
  { itemId: 3, itemName: "Suitcase 650", price: 350, initialAvailableQuantity: 2 },
  { itemId: 4, itemName: "Suitcase 1050", price: 550, initialAvailableQuantity: 5 },
];

// Helper function to get item by id
function getItemById(id) {
  return listProducts.find(product => product.itemId === id);
}

// Function to reserve stock for an item by its id
async function reserveStockById(itemId, stock) {
  await setAsync(`item.${itemId}`, stock);
}

// Function to get the current reserved stock by item id
async function getCurrentReservedStockById(itemId) {
  const reservedStock = await getAsync(`item.${itemId}`);
  return reservedStock ? parseInt(reservedStock, 10) : 0;
}

// Route: List all products
app.get('/list_products', (req, res) => {
  const products = listProducts.map(product => ({
    itemId: product.itemId,
    itemName: product.itemName,
    price: product.price,
    initialAvailableQuantity: product.initialAvailableQuantity,
  }));
  res.json(products);
});

// Route: Get details of a single product
app.get('/list_products/:itemId', async (req, res) => {
  const productId = parseInt(req.params.itemId, 10);
  const product = getItemById(productId);

  if (!product) {
    return res.json({ status: 'Product not found' });
  }

  const reservedStock = await getCurrentReservedStockById(productId);
  const availableStock = product.initialAvailableQuantity - reservedStock;

  res.json({
    itemId: product.itemId,
    itemName: product.itemName,
    price: product.price,
    initialAvailableQuantity: product.initialAvailableQuantity,
    currentQuantity: availableStock,
  });
});

// Route: Reserve a product
app.get('/reserve_product/:itemId', async (req, res) => {
  const productId = parseInt(req.params.itemId, 10);
  const product = getItemById(productId);

  if (!product) {
    return res.json({ status: 'Product not found' });
  }

  const reservedStock = await getCurrentReservedStockById(productId);
  const availableStock = product.initialAvailableQuantity - reservedStock;

  if (availableStock < 1) {
    return res.json({ status: 'Not enough stock available', itemId: productId });
  }

  // Reserve the stock
  await reserveStockById(productId, reservedStock + 1);

  res.json({ status: 'Reservation confirmed', itemId: productId });
});

// Start the server
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
