import React from 'react'

export const SearchByTags = () => {
  return (
    <div>
      <div to="/" className="text-2xl font-bold mb-4">
          <span className='bg-text-1 text-white px-1 me-1'>Search</span>
          <span className='text-[15px] font-light'>With Tags</span>
      </div>
      <div className='flex flex-row gap-2 text-text-2 font-light flex-wrap'>
        <span className='py-0 px-2 border rounded border-text-8'>Travel</span>
        <span className='py-0 px-2 border rounded border-text-8'>Lifestyle</span>
        <span className='py-0 px-2 border rounded border-text-8'>Technology</span>
        <span className='py-0 px-2 border rounded border-text-8'>Food</span>
        <span className='py-0 px-2 border rounded border-text-8'>Fashion</span>
        <span className='py-0 px-2 border rounded border-text-8'>Sports</span>
        <span className='py-0 px-2 border rounded border-text-8'>Music</span>
        <span className='py-0 px-2 border rounded border-text-8'>Health</span>
        <span className='py-0 px-2 border rounded border-text-8'>Science</span>

      </div>
    </div>
  )
}
