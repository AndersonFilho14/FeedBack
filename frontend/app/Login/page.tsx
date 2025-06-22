

export default function Login() {


    return(<>
        
        <body>
            <header className="bg-green-300 border-red-400 border-5 text-lg text-center">IMD-IA</header>
            <div className="flex justify-center items-center h-screen bg-gradient-to-r from-emerald-500 to-emerald-800">
                <main className="bg-white border-amber-700 p-8 rounded-3xl shadow-md w-96 flex flex-col items-center border-5">
                    <h1 className="mb-4">Bem Vindo!</h1>
                    <h5>Login</h5>
                    <input className="bg-emerald-700 mb-4 w-64 h-8 rounded" type="text" name="User" id="" />
                    <h5>Senha</h5>
                    <input className=" bg-emerald-700 mb-4 w-64 h-8 rounded" type="text" name="password" />
                    <button className=" border-amber-700 border-5">Entrar</button>
                </main>
            </div>
        </body>
    </>
    );
}