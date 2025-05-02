import React, { useState } from 'react';

// Компонент страницы регистрации
function Register({ togglePage }) {
    const [nickname, setNickname] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:8000/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nickname, password })
            });
            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('token', data.access_token);
                // TODO: Перенаправить на страницу игрока
                alert('Регистрация успешна!');
            } else {
                setError('Никнейм уже занят');
            }
        } catch (err) {
            setError('Ошибка сервера');
        }
    };

    return (
        <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
            <h2 className="text-2xl font-bold mb-6 text-center">Регистрация</h2>
            {error && <p className="text-red-500 mb-4">{error}</p>}
            <form onSubmit={handleSubmit}>
                <div className="mb-4">
                    <label className="block text-gray-700 mb-2" htmlFor="nickname">Никнейм</label>
                    <input
                        type="text"
                        id="nickname"
                        value={nickname}
                        onChange={(e) => setNickname(e.target.value)}
                        className="w-full p-2 border rounded"
                        required
                    />
                </div>
                <div className="mb-6">
                    <label className="block text-gray-700 mb-2" htmlFor="password">Пароль</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="w-full p-2 border rounded"
                        required
                    />
                </div>
                <button type="submit" className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600">
                    Зарегистрироваться
                </button>
            </form>
            <p className="mt-4 text-center">
                Уже есть аккаунт?{' '}
                <button onClick={togglePage} className="text-blue-500 hover:underline">
                    Войти
                </button>
            </p>
        </div>
    );
}

export default Register;