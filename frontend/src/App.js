import React, { useState } from 'react';
import Login from './components/Login';
import Register from './components/Register';

// Главный компонент приложения
function App() {
    const [isLogin, setIsLogin] = useState(true);

    return (
        <div className="min-h-screen bg-gray-100 flex items-center justify-center">
            {isLogin ? (
                <Login togglePage={() => setIsLogin(false)} />
            ) : (
                <Register togglePage={() => setIsLogin(true)} />
            )}
        </div>
    );
}

export default App;