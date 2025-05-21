import { useState, useEffect } from 'react';
import axios from 'axios';

export default function Home() {
  const [items, setItems] = useState([]);
  const [newItem, setNewItem] = useState({ name: '', description: '' });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8888';
  
  useEffect(() => {
    const fetchItems = async () => {
      try {
        const response = await axios.get(`${apiUrl}/items/`);
        setItems(response.data.items);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching items:', err);
        setError('Failed to fetch items');
        setLoading(false);
      }
    };
    
    fetchItems();
  }, [apiUrl]);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${apiUrl}/items/`, newItem);
      setItems([...items, response.data]);
      setNewItem({ name: '', description: '' });
    } catch (err) {
      console.error('Error creating item:', err);
      setError('Failed to create item');
    }
  };
  
  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h1>Items Management</h1>
      
      <div style={{ marginBottom: '20px' }}>
        <h2>Add New Item</h2>
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '10px' }}>
            <label htmlFor="name">Name: </label>
            <input
              type="text"
              id="name"
              value={newItem.name}
              onChange={(e) => setNewItem({ ...newItem, name: e.target.value })}
              required
              style={{ marginLeft: '10px' }}
            />
          </div>
          <div style={{ marginBottom: '10px' }}>
            <label htmlFor="description">Description: </label>
            <input
              type="text"
              id="description"
              value={newItem.description}
              onChange={(e) => setNewItem({ ...newItem, description: e.target.value })}
              style={{ marginLeft: '10px' }}
            />
          </div>
          <button type="submit" style={{ padding: '5px 10px' }}>Add Item</button>
        </form>
      </div>
      
      <div>
        <h2>Items List</h2>
        {loading ? (
          <p>Loading items...</p>
        ) : error ? (
          <p style={{ color: 'red' }}>{error}</p>
        ) : items.length === 0 ? (
          <p>No items found. Add some items above!</p>
        ) : (
          <ul>
            {items.map((item) => (
              <li key={item.id}>
                <strong>{item.name}</strong>: {item.description}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}