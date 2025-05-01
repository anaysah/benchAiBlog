import { useState } from "react";
import SignupForm from "../components/ui/SignupForm";
import LoginForm from "../components/ui/LoginForm";

function Auth() {
  const [isLogin, setIsLogin] = useState(true);

  return (
    <div className="mx-auto p-4 min-h-[90vh] flex flex-col items-center justify-center">
      {isLogin ? <LoginForm /> : <SignupForm />}

      <div className="mt-4 text-center">
        {isLogin ? (
          <>
            <span>Don't have an account? </span>
            <button
              className="text-blue-600 underline"
              onClick={() => setIsLogin(false)}
            >
              Sign up
            </button>
          </>
        ) : (
          <>
            <span>Already have an account? </span>
            <button
              className="text-blue-600 underline"
              onClick={() => setIsLogin(true)}
            >
              Log in
            </button>
          </>
        )}
      </div>
    </div>
  );
}

export default Auth;
