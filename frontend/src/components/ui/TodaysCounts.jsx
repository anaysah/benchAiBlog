import React from 'react'

const TodaysCounts = () => {
  return (
    <div>
        <div to="/" className="text-2xl font-bold mb-4">
            <span className='bg-text-1 text-white px-1 me-1'>Today's</span>
            <span className='text-[15px] font-light'>Counts</span>
        </div>
        <div className="flex flex-wrap text-text-1">
            <div className="w-1/2 px-2 mb-4 box-border">
                <div className="bg-back-2 rounded flex flex-col justify-center items-center py-4">
                <span className='font-bold'>14</span>
                <span>New Posts</span>
                </div>
            </div>
            <div className="w-1/2 px-2 mb-4 box-border">
                <div className="bg-back-2 rounded flex flex-col justify-center items-center py-4">
                <span className='font-bold'>480</span>
                <span>Total Visitors</span>
                </div>
            </div>
            <div className="w-1/2 px-2 mb-4 box-border">
                <div className="bg-back-2 rounded flex flex-col justify-center items-center py-4">
                <span className='font-bold'>139</span>
                <span>Blog Read</span>
                </div>
            </div>
        </div>

    </div>
  )
}

export default TodaysCounts