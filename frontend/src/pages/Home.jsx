import { useState, useEffect } from 'react';
import axios from 'axios';
import { BlogPostCard } from '../components/ui/BlogPostCard';
import { TopAuthers } from '../components/ui/TopAuthers';

function Home() {
  const [blogs, setBlogs] = useState([]);

  useEffect(() => {
    const fetchBlogs = async () => {
      try {
        const response = await axios.get('/api/blogs/posts');
        setBlogs(response.data.results);
        console.log(response.data);
      } catch (error) {
        console.error('Error fetching blogs:', error);
      }
    };

    fetchBlogs();
  }, []);

  return (
    <div className="container mx-auto p-5 flex gap-4 ">
      <div className="basis-[70%] flex flex-col gap-4">
        {blogs.length > 0 ? (
          blogs.map((blog) => <BlogPostCard key={blog.id} blog={blog} />)
        ) : (
          <div className="text-gray-500">No blog posts found.</div>
        )}
      </div>
      <div className="basis-[30%] p-5">
        <TopAuthers/>
      </div>
    </div>
  );
}

export default Home;
