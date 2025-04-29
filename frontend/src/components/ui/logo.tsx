import { Link } from "react-router-dom"
import React from "react"

export const Logo = () => {
  return(
    <>
      <Link to="/" className="text-2xl font-bold">
        <span className='bg-text-1 text-white px-1 me-1'>Note</span>
        <span className='text-[15px] font-light'>Book</span>
      </Link>
    </>
  )
}
