

export default function Login() {


    return(<>
            
        <body>
            <header className="font-[InknutAntiqua] bg-[#727D73] border-[#A4B465] text-[#EEA03D] border-7 h-21  text-center text-7xl ">IMD-IA</header>
            <div className="bg-[#F5ECD5] bg-[url('/imagem/backgroundloginimage.png')] bg-cover bg-center bg-no-repeat  flex justify-center items-center h-screen ">
                <main className="font-[Jomolhari] bg-[#F5ECD5] border-[#A7C1A8] w-96 h-123  rounded-3xl shadow-[0_16px_7.8px_2px_rgba(0,0,0,0.25)]  flex flex-col items-center border-11 ">
                    <h1 className="text-[#EEA03D]  mt-16 mb-16 text-6xl ">Bem Vindo!</h1>
                    <h5 className="mb-px">Usuario</h5>
                    <input className="bg-[#A7C1A8] mb-4 pl-2 w-80 h-10 rounded inset-shadow-[0_2px_1.8px_1px_rgba(0,0,0,0.25)]" type="text" name="User" id="" />
                    <h5>Senha</h5>
                    <input className=" bg-[#A7C1A8] mb-4 pl-2 w-80 h-10 rounded inset-shadow-[0_2px_1.8px_1px_rgba(0,0,0,0.25)]" type="text" name="password" />
                    <span className=" cursor-pointer mt-4 flex flex-col items-center p-[7] bg-[#727D73] rounded-xl shadow-[0_4px_20px_0_rgba(0,0,0,0.25)]">
                        <button className=" cursor-pointer pt-2 pb-2 pl-14 pr-14 bg-[#D0DDD0] border-[#727D73] rounded-sm">Entrar</button>
                    </span>  
                </main>
            </div>  
        </body>
    </>
    );
}