import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { ChatSender } from "@/models/chat";

type LoadingBubbleProps = {
  chatSender: ChatSender;
};

export const LoadingBubble: React.FC<LoadingBubbleProps> = ({ chatSender }) => {
  return (
    <>
      <div
        className={`flex flex-col ${
          chatSender === ChatSender.USER && "items-end"
        } my-2`}
      >
        <div className={`flex gap-2 mb-2`}>
          {chatSender === ChatSender.BOT && (
            <Avatar>
              <AvatarImage
                src="https://api.dicebear.com/9.x/micah/svg?seed=Boo"
                alt="Ava"
              />
              <AvatarFallback>Ava</AvatarFallback>
            </Avatar>
          )}
          {chatSender === ChatSender.BOT ? (
            <div className=" bg-gray-200 dark:bg-gray-700 p-4 rounded-3xl rounded-tl-none max-w-48">
              <div className="flex flex-col gap-2 animate-pulse">
                <div className="rounded-full bg-slate-600 h-2"></div>
                <div className="rounded-full bg-slate-600  h-2"></div>
                <div className="rounded-full bg-slate-600  h-2"></div>
              </div>
            </div>
          ) : (
            <div className="bg-purple-600 dark:bg-purple-200 p-4 rounded-3xl rounded-tr-none text-white dark:text-black w-72">
              <div className="flex flex-col gap-2 animate-pulse">
                <div className="rounded-full bg-purple-300 h-2"></div>
                <div className="rounded-full bg-purple-300  h-2"></div>
                <div className="rounded-full bg-purple-300 h-2"></div>
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
};
