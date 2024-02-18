import { useContext } from "react";
import AppContext from "../AppContext";
import { HiSparkles } from "react-icons/hi";

const FormComponent = () => {
    const { isActive, setIsActive } = useContext(AppContext);
    // console.log(isActive);
    const handleClick = () => {
        // console.log(isActive);
        setIsActive(true);
        console.log(isActive);
    };
    return (
        <div className={`width-100 bg-transparent px-7 py-2 flex flex-col justify-between ${isActive ? 'h-[20vh]' : 'h-[85vh]'}`}>
            <div className={`${isActive ? 'hidden' : 'w-full'}`}>
                <div className="w-[350px] text-transparent font-semibold text-6xl ml-8 mt-7 bg-gradient-to-r from-[#5581eb] via-[#f72798] to-[#ffa60b] bg-clip-text">
                    Hello Varun,
                </div>
            </div>
            <div className={`font-semibold text-4xl ml-8 mt-4 text-[#343479] ${isActive ? 'hidden' : 'w-full'}`}>
                Please enter your prompt.
            </div>
            <div className = {`!transition-all duration-5000 ${isActive ? 'h-[100%]' : 'h-auto'} ${isActive ? 'mt-0 !important' : 'mt-auto !important'}`}>
                <div className={`flex flex-col gap-4 rounded-lg ${isActive ? 'mb-2' : 'mb-6'}`}>
                    <div className="grid grid-cols-3 gap-0 rounded-2xl bg-[#161646] py-2 shadow-lg">
                        <div className={`${isActive ? 'h-[60px]' : 'h-[80px]'} w-full bg-[#161646] rounded-l-3xl border-r-2 border-[#9290C3] border-opacity-50`}>
                            <input
                                placeholder="text"
                                className="bg-[#161646] w-full h-full rounded-l-3xl outline-none text-[#9290C3] p-5 overflow-y-auto text-opacity-70 max-w-300"
                            />
                        </div>
                        <div className={`${isActive ? 'h-[60px]' : 'h-[80px]'} w-full bg-[#161646]`}>
                            <input
                                placeholder="constraints"
                                className="bg-[#161646] w-full h-full outline-none text-[#9290C3] p-5 overflow-y-autotext-opacity-70"
                            />
                        </div>
                        <div className={`${isActive ? 'h-[60px]' : 'h-[80px]'} w-full bg-[#161646] rounded-r-3xl border-l-2 border-[#9290C3] border-opacity-50`}>
                            <input
                                placeholder="schema"
                                className="bg-[#161646] w-full h-full rounded-r-3xl outline-none text-[#9290C3] p-5 overflow-y-autotext-opacity-70"
                            />
                        </div>
                    </div>
                    <button
                        type="button"
                        className={`bg-[#9290C3] rounded-lg px-5 py-2 text-[#161646] font-bold mx-auto hover:bg-[#6d6b91] flex flex-row transition ${isActive ? 'transition-opacity duration-200 opacity-0' : 'transition-opacity duration-200 opacity-100'}`}
                        onClick={handleClick}
                    >
                        Generate <HiSparkles className="my-auto ml-1 mt-1.25" />
                    </button>
                </div>
            </div>
        </div>
    );
}

export default FormComponent;