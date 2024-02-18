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
                    <p className="text-left p-3 pt-0 px-4">
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Rhoncus urna neque viverra justo nec ultrices dui sapien. Vitae ultricies leo integer malesuada. Rhoncus urna neque viverra justo nec ultrices. Auctor neque vitae tempus quam pellentesque. Risus in hendrerit gravida rutrum quisque non tellus orci ac. At volutpat diam ut venenatis tellus in metus vulputate eu. Duis tristique sollicitudin nibh sit amet commodo nulla facilisi nullam. Semper viverra nam libero justo laoreet sit amet. Neque gravida in fermentum et sollicitudin ac orci phasellus. Mattis molestie a iaculis at erat. Sit amet consectetur adipiscing elit pellentesque. In nulla posuere sollicitudin aliquam ultrices sagittis orci a scelerisque. A diam maecenas sed enim ut sem viverra. Vitae congue eu consequat ac felis
                    </p>
                </div>
                {/* <div className="h-[250px] text-center text-sm font-bold pt-8 text-[#161646] mx-auto rounded-lg bg-[#9290C3] w-[900px]">
                    message
                </div> */}
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