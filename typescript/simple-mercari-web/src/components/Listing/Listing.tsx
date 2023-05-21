import React, { useState } from 'react';

const server = process.env.REACT_APP_API_URL || 'http://127.0.0.1:9000';

interface Prop {
  onListingCompleted?: () => void;
}

type formDataType = {
  name: string,
  category: string,
  image: string | File,
}

export const Listing: React.FC<Prop> = (props) => {
  const { onListingCompleted } = props;
  const initialState = {
    name: "",
    category: "",
    image: "",
  };
  const [values, setValues] = useState<formDataType>(initialState);
  const [formRef, setFormRef] = useState<any>();

  const onValueChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setValues({
      ...values, [event.target.name]: event.target.value,
    })
  };
  const onFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setValues({
      ...values, [event.target.name]: event.target.files![0],
    })
  };
  const onSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    const data = new FormData()
    data.append('name', values.name)
    data.append('category', values.category)
    data.append('image', values.image)

    fetch(server.concat('/items'), {
      method: 'POST',
      mode: 'cors',
      body: data,
    })
      .then(response => {
        console.log('POST status:', response.statusText);
        setValues(initialState); // reset form here
        formRef && formRef.reset(); // reset file input here
        onListingCompleted && onListingCompleted();
      })
      .catch((error) => {
        console.error('POST error:', error);
      })
  };
  return (
    <div className='Listing'>
      <form ref={e => setFormRef(e)} onSubmit={onSubmit}>
        <div className="listing-form">
          <input type='text' name='name' id='name' placeholder='name' onChange={onValueChange} value={values.name} required />
          <input type='text' name='category' id='category' placeholder='category' onChange={onValueChange} value={values.category} />
          {/* <label htmlFor="image" >
            <button className="form-img-btn">Upload Image</button>
          </label> */}
          <input className="custom-file-upload" type="file" name="image" id="image" onChange={onFileChange} required />

          <button className ="form-btn" type='submit'>List this item</button>
        </div>
      </form>
    </div>
  );
}
