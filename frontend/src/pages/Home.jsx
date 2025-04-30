import { useState, useEffect } from 'react';
import axios from 'axios';
import { BlogPostCard } from '../components/ui/BlogPostCard';
import { TopAuthers } from '../components/ui/TopAuthers';
import { SideBarAdCard } from '../components/ui/SideBarAdCard';
import SideBarCategoriesCount from '../components/ui/SideBarCategoriesCount';
import TodaysCounts from '../components/ui/TodaysCounts';
import { SearchByTags } from '../components/ui/SearchByTags';

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
      <div className="basis-[30%] p-5 gap-5 flex flex-col">
        <TopAuthers/>
        <SideBarAdCard/>
        <SideBarCategoriesCount/>
        <TodaysCounts/>
        <SearchByTags/>
      </div>
    </div>
  );
}

export default Home;
