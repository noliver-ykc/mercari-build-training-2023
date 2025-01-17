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

export const ItemList: React.FC<Prop> = (props) => {
  const { reload = true, onLoadCompleted } = props;
  const [items, setItems] = useState<Item[]>([])
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
        const reversedItems = data.items.reverse();
        const slicedItems = reversedItems.slice(1); // Skip the most recent item
        setItems(slicedItems);
        onLoadCompleted && onLoadCompleted();
      })
  }


  useEffect(() => {
    if (reload) {
      fetchItems();
    }
  }, [reload]);

  return (
    <div className="itemsGrid">
      {items.map((item) => {
        return (
          <div key={item.id} className='ItemList'>
            <img className="item-img"src={`http://localhost:9000/image/${item.image_filename}`} alt="item"/>
            <div className="item-info">
              <span className="item-name">{item.name}</span>
              <br />
              <span className="item-category">#{item.category}</span>
            </div>
          </div>
        )
      })}
    </div>
  )
};
