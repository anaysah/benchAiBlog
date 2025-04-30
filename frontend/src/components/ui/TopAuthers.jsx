import React from 'react'
import { FacebookIcon, InstagramIcon, LinkedInIcon, TwitterIcon } from "../common/icons";
import authorImg from './Rectangle 3003.png'


const AutherCard = () => {
  return (
    <div className='flex flex-row gap-4'>
        <div>
          <img src={authorImg}/>
        </div>
        <div className='flex flex-col  text-text-2'>
          <span className='text-text-4'>Jenny Kia</span>
          <span className='text-sm font-extralight'>Fashion designer, Blogger, activist</span>
          <div className='flex flex-row gap-2 mt-2'>
            <span><TwitterIcon className='w-4 h-4'/></span>
            <span><InstagramIcon className='w-4 h-4 '/></span>
            <span><LinkedInIcon className='w-4 h-4'/></span>
            <span><FacebookIcon className='w-4 h-4'/></span>
          </div>
        </div>
    </div>
  )
}


export const TopAuthers = () => {
  return (
    <div>
        <div to="/" className="text-2xl font-bold mb-4">
            <span className='bg-text-1 text-white px-1 me-1'>Top</span>
            <span className='text-[15px] font-light'>Authers</span>
        </div>
        <div className='flex flex-col gap-4'>
            <AutherCard/>
            <AutherCard/>
            <AutherCard/>
        </div>
    </div>
  )
}
