import React, { useEffect, useState } from 'react';

interface Item {
  id: number;
  name: string;
  category: string;
  image_filename: string;
};

const server = process.env.REACT_APP_API_URL || 'http://127.0.0.1:9000';

interface Prop {
  reload?: boolean;
  onLoadCompleted?: () => void;
}
export const ItemCallout: React.FC<Prop> = (props) => {
  const { reload = true, onLoadCompleted } = props;
  const [item, setItem] = useState<Item | null>(null);

  const fetchItems = () => {
    fetch(server.concat('/items'), {
      method: 'GET',
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
    })
      .then(response => response.json())
      .then(data => {
        console.log('GET success:', data);
        const mostRecentItem = data.items[data.items.length - 1];
        setItem(mostRecentItem);
        onLoadCompleted && onLoadCompleted();
      })
      .catch(error => {
        console.error('GET error:', error)
      });
  }

  useEffect(() => {
    if (reload) {
      fetchItems();
    }
  }, [reload]);

  return (
    <div className="featured">
      {item && (
        <div key={item.id} className='featured-item'>
          <img className="featured-img"src={`http://localhost:9000/image/${item.image_filename}`} alt="item"/>
          <div className="featured-item-text">
            <p className="featured-item-name">{item.name}</p>
            <p className="featured-item-category">#{item.category}</p>
          </div>

        </div>

      )}
    </div>
  );
};
