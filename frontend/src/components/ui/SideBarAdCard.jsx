import React from 'react'

export const SideBarAdCard = () => {
  return (
    <div className='relative flex justify-center items-center p-8 text-white bg-text-1'>
      {/* AD badge */}
      <span className='absolute top-2 right-2 text-xs bg-white text-text-1 px-2 py-0.5 rounded font-semibold shadow'>
        Ad
      </span>
        <div className='pr-10 flex flex-col justify-start'>
            <span className='font-bold text-xl'>Want to travel sikkim by car?</span>
            <span className='font-light text-sm'>Did you come here for something in particular or just general Riker-bashing? And blowing into</span>
            <span className='mt-5 bg-white text-text-1 p-2 py-1 self-start rounded'>Visit Us</span>
        </div>
    </div>
  )
}
