import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter, Navigate, Routes, Route } from 'react-router-dom';
import './App.css'
import ChatsPage from './components/ChatsPage';

const queryClient = new QueryClient();

function NotFound() {
  return <h1>404: not found</h1>;
}

function ErrorPage() {
  return (
    <>
      <h1>an error has occurred</h1>
      <p>contact site admin for support</p>
    </>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          {/* Main Routs */}
          <Route path="/" element={<ChatsPage />} />
          <Route path="/chats" element={<ChatsPage />} />
          <Route path="/chats/:chatId" element={<ChatsPage />} />

          {/* Errors */}
          <Route path="/error" element={<ErrorPage />} />
          <Route path="/error/404" element={<NotFound />} />
          <Route path="*" element={<Navigate to="/error/404" />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App
