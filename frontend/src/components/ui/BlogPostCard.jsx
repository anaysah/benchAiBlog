import React from 'react'

export const BlogPostCard = ({ blog }) => {
  if (!blog) return null

  const {
    title,
    thumbnail,
    snippet,
    date,
    category,
  } = blog

  const formattedDate = new Date(date).toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })

  return (
    <div className='flex gap-4 p-4 md:flex-row h-full'>
      <div className='flex-1'>
        <img
          src={thumbnail}
          alt='Blog Thumbnail'
          className='w-full h-48 object-cover rounded-lg'
        />
      </div>
      <div className='flex-1 flex flex-col gap-1'>
        <span className='bg-back-3 text-sm font-light px-2 py-1 rounded text-text-2 w-fit'>
          {category?.name || 'Uncategorized'}
        </span>
        <div className='font-semibold text-xl text-gray-800'>
          {title}
        </div>
        <div className='text-sm text-gray-500 flex gap-2'>
          <span>{formattedDate}</span>
          <span>•</span>
          <span>5 min read</span>
        </div>
        <span className='text-gray-700 text-sm'>
          {snippet}
        </span>
        <div className='flex justify-end flex-1 '>
          <button className='self-end px-4 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700 transition'>
            Read
          </button>
        </div>
      </div>
    </div>
  )
}
