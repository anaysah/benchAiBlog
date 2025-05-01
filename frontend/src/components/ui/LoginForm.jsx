import React from 'react';
import { Link } from 'react-router-dom';

const preventRefresh = (e) => {
	e.preventDefault();
};

export default function LoginForm() {
	return (
		<div className="w-[30%] flex  flex-col justify-center bg-white rounded-xl shadow-md p-8">
			<h2 className="text-2xl font-bold text-center text-gray-800 mb-6">Login</h2>
			<form className='flex flex-col flex-wrap gap-4 items-stretch'>
				<div className="">
					<label htmlFor="e-mail" className="block text-sm font-medium text-gray-700 mb-1">
						E-Mail
					</label>
					<input
						type="email"
						id="e-mail"
						placeholder="Enter your email"
						className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
					/>
				</div>

				<div className="">
					<label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
						Password
					</label>
					<input
						type="password"
						id="password"
						placeholder="@#$%!@"
						className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
					/>
				</div>

				<button
					type="submit"
					onClick={preventRefresh}
					className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition-colors"
				>
					Submit
				</button>
			</form>
		</div>
	);
}
