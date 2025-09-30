import { useState } from 'react'
import {AuthProvider} from "./contexts/AuthContext.tsx";
import AuthButton from "./components/AuthButton.tsx";
import ProtectedRoute from './components/ProtectedRoute.tsx'
import TodoApp from "./components/TodoApp.tsx";

function App() {
 return (
        <AuthProvider>
            <div className="min-h-screen bg-gray-100">
                <header className="bg-white shadow-sm border-b">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div className="flex justify-between items-center py-4">
                            <h1 className="text-2xl font-bold text-gray-900">
                                Todo App
                            </h1>
                            <AuthButton />
                        </div>
                    </div>
                </header>

                <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
                    {/*<ProtectedRoute>*/}
                        <TodoApp />
                    {/*</ProtectedRoute>*/}
                </main>
            </div>
        </AuthProvider>
    );
}

export default App
