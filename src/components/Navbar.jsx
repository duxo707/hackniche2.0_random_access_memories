import { FaBars } from  "react-icons/fa";
import BotIcon from "./BotIcon";

const Navbar = () => {
    return (
        <div className="width-[100vw] 
            px-9
            pt-4 
            pb-4 
            flex 
            justify-between 
            items-center 
            bg-transparent
            text-[#9290C3]
            h-[15vh]
        ">
            <div className="flex flex-row">
                <h1 className="font-bold text-xl">Codegen</h1>
            </div>
            <button className="align-self-right text-xl">
                <FaBars />
            </button>
        </div>
    );
}

export default  Navbar;