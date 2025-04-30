import React from 'react'

const SideBarCategoriesCount = () => {
  return (
    <div>
        <span className='bg-text-1 text-white px-1 text-2xl font-bold mb-4 font-semibold'>Categories</span>
        <div className='text-text-6 mt-5 flex flex-col font-semibold '>
          <span className='flex justify-between border-b border-dashed border-text-7 py-3'><span>LifeStyle</span><span>09</span></span>
          <span className='flex justify-between border-b border-dashed border-text-7 py-3'><span>Travel</span><span>21</span></span>
          <span className='flex justify-between border-b border-dashed border-text-7 py-3'><span>Food</span><span>15</span></span>
          <span className='flex justify-between border-b border-dashed border-text-7 py-3'><span>Health</span><span>07</span></span>
        </div>
    </div>
  )
}

export default SideBarCategoriesCount