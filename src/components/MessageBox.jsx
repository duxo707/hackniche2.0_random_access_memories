import { useContext } from "react";
import AppContext from "../AppContext";
import { IoIosSend } from "react-icons/io";


const MessageBox = () => {
    const { isActive, setIsActive } = useContext(AppContext);    
    if (isActive)
    console.log(isActive);
    return (
        <div className={`flex flex-col pb-4 w-[100vw] mt-1 ${isActive ? 'h-[65vh]' : 'h-0'}`}>
            <div className="overflow-y-auto mb-2">
                <div className="h-[250px] text-center text-sm font-bold pt-8 mb-4 text-[#161646] mx-auto rounded-lg bg-[#9290C3] w-[900px]">
                    message
                </div>
                <div className="h-[250px] text-center text-sm font-bold pt-8 text-[#161646] mx-auto rounded-lg bg-[#9290C3] w-[900px]">
                    message
                </div>
            </div>
            <div className="mt-auto mx-3 flex flex-row mb-2">
                <input 
                    placeholder="Type a prompt.."
                    className="w-[100%] mx-2 px-4 py-2 rounded-xl border-[#9290C3] bg-[#161646] text-[#9290C3] outline-none"
                />
                <button 
                    type="button" 
                    className="rounded-full bg-[#9290C3] mx-2 py-3 px-3 text-[#161646]"
                >
                    <IoIosSend className="text-2xl" />
                </button>
            </div>
        </div>
    );
}

export default  MessageBox;