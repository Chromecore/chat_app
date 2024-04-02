import LeftNav from "./LeftNav";
import ChatPage from './ChatPage';

function ChatsPage() {
    return (
        <div className="flex flex-row h-main">
            <div className="w-40">
                <LeftNav />
            </div>
            <div className="mx-auto pt-8">
                <ChatPage />
            </div>
        </div>
    );
}

export default ChatsPage;