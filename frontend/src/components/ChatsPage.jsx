import LeftNav from "./LeftNav";
import ChatPage from './ChatPage';

function ChatsPage() {
    return (
        <div className="flex flex-row h-main">
            <LeftNav className="w-40" />
            <ChatPage className="m-1" />
        </div>
    );
}

export default ChatsPage;