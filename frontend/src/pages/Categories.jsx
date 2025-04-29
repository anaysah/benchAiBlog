import React from 'react'
import { useState, useEffect } from 'react';
import axios from 'axios';

export const CategoryBox = ({ name, svg }) => {
  console.log('SVG Content:', svg);
    return (
      <div className="flex flex-col items-center justify-center p-4  rounded-md bg-back-1 px-20">
        <div
          className=" mb-2 flex flex-col items-center justify-center text-text-1"
          dangerouslySetInnerHTML={{ __html: svg }}
        />
        <div className="text-sm font-medium text-center text-text-4">
          {name}
        </div>
      </div>
    );
  };
  


function Categories() {
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await axios.get('/api/blogs/categories/');
        setCategories(response.data.results);
        console.log(response.data);
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    };

    fetchCategories();
  }, []);
  

    return (
      <div className="container mx-auto p-4">
        <h1 className="text-3xl font-bold text-center text-[27px] text-text-4 mb-5">Categories</h1>
        <div className='flex justify-center flex-wrap gap-4'>
          {categories.map((category) => (
            <CategoryBox
              key={category.id}
              name={category.name}
              svg={category.icon_svg}
            />
          ))}
        </div>

      </div>
    );
  }
  
  export default Categories;