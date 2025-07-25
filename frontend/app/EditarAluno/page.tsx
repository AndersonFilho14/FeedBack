"use client";
import React, { useState, useEffect, useCallback } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";

// --- Interfaces de Dados ---
// Define a estrutura completa dos dados do aluno, alinhada com o modelo do backend
interface AlunoData {
    id: number;
    nome: string;
    cpf: string;
    data_nascimento: string;
    sexo: string;
    nacionalidade: string;
    faltas: number;
    id_turma?: number | null;
    id_responsavel: number;
    etnia?: number | null;
    educacaoPais?: number | null;
    tempoEstudoSemanal?: number | null;
    apoioPais: number;
    aulasParticulares: number;
    extraCurriculares: number;
    esportes: number;
    aulaMusica: number;
    voluntariado: number;
    // Dados do responsável, que podem ser enviados juntos
    nome_responsavel: string;
    numero_responsavel: string;
}

interface TurmaData {
    id: number;
    nome: string;
}

// --- Mapeamentos para Selects (Dropdowns) ---
// Melhora a clareza do código ao invés de usar "números mágicos"
const etniaOptions = [
    { value: 1, label: "Branca" },
    { value: 2, label: "Preta" },
    { value: 3, label: "Parda" },
    { value: 4, label: "Amarela" },
    { value: 5, label: "Indígena" },
    { value: 99, label: "Não declarado" },
];

const educacaoPaisOptions = [
    { value: 0, label: "Nenhuma" },
    { value: 1, label: "Fundamental" },
    { value: 2, label: "Médio" },
    { value: 3, label: "Superior" },
    { value: 4, label: "Pós-graduação" },
];


export default function EditarAluno() {
    const searchParams = useSearchParams();
    const alunoId = searchParams.get("id");
    
    // --- Estados do Formulário ---
    // Dados Pessoais
    const [nome, setNome] = useState("");
    const [data, setData] = useState("");
    const [sexo, setSexo] = useState("");
    const [cpf, setCpf] = useState("");
    const [nacionalidade, setNacionalidade] = useState("");
    const [etnia, setEtnia] = useState<string>("");

    // Dados do Responsável
    const [nomeResponsavel, setNomeResponsavel] = useState("");
    const [telefoneResponsavel, setTelefoneResponsavel] = useState("");

    // Dados Acadêmicos e Comportamentais
    const [idTurma, setIdTurma] = useState<string>("");
    const [faltas, setFaltas] = useState<string>("0");
    const [educacaoPais, setEducacaoPais] = useState<string>("");
    const [tempoEstudoSemanal, setTempoEstudoSemanal] = useState<string>("");
    
    // Checkboxes (true/false)
    const [apoioPais, setApoioPais] = useState(false);
    const [aulasParticulares, setAulasParticulares] = useState(false);
    const [extraCurriculares, setExtraCurriculares] = useState(false);
    const [esportes, setEsportes] = useState(false);
    const [aulaMusica, setAulaMusica] = useState(false);
    const [voluntariado, setVoluntariado] = useState(false);

    const [turmas, setTurmas] = useState<TurmaData[]>([]);

    // --- Estados de Controle da UI ---
    const [loading, setLoading] = useState(true);
    const [isSaving, setIsSaving] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [message, setMessage] = useState<string | null>(null);

    // --- Busca de Dados ---
    const fetchAlunoData = useCallback(async () => {
        if (!alunoId) {
            setError("ID do aluno não foi fornecido na URL.");
            setLoading(false);
            return;
        }
        setLoading(true);
        setError(null);
        
        try {
            // Busca dados do aluno e turmas da escola em paralelo para otimizar
            const [alunoResponse, turmasResponse] = await Promise.all([
                fetch(`http://localhost:5000/aluno/${alunoId}`),
                fetch(`http://localhost:5000/turmas/escola/1`) // Hardcoded para escola 1
            ]);

            if (!alunoResponse.ok) throw new Error("Falha ao buscar dados do aluno.");
            if (!turmasResponse.ok) throw new Error("Falha ao buscar lista de turmas.");
            
            const aluno: AlunoData = await alunoResponse.json();
            const turmasData: { turmas: TurmaData[] } = await turmasResponse.json();
            
            setTurmas(turmasData.turmas || []);

            // Preenche o formulário com os dados do aluno
            setNome(aluno.nome || "");
            setCpf(aluno.cpf || "");
            setData(aluno.data_nascimento ? aluno.data_nascimento.split('T')[0] : "");
            setSexo(aluno.sexo || "");
            setNacionalidade(aluno.nacionalidade || "");
            setEtnia(aluno.etnia?.toString() || "");
            setIdTurma(aluno.id_turma?.toString() || "");
            setFaltas(aluno.faltas?.toString() || "0");
            
            // Dados do responsável
            // TODO: Ajustar para buscar o responsável pelo `id_responsavel` se a API permitir
            setNomeResponsavel(aluno.nome_responsavel || "");
            setTelefoneResponsavel(aluno.numero_responsavel || "");

            // Dados adicionais
            setEducacaoPais(aluno.educacaoPais?.toString() || "");
            setTempoEstudoSemanal(aluno.tempoEstudoSemanal?.toString() || "");
            setApoioPais(aluno.apoioPais === 1);
            setAulasParticulares(aluno.aulasParticulares === 1);
            setExtraCurriculares(aluno.extraCurriculares === 1);
            setEsportes(aluno.esportes === 1);
            setAulaMusica(aluno.aulaMusica === 1);
            setVoluntariado(aluno.voluntariado === 1);

        } catch (err: any) {
            setError(err.message || "Ocorreu um erro inesperado.");
        } finally {
            setLoading(false);
        }
    }, [alunoId]);

    useEffect(() => {
        fetchAlunoData();
    }, [fetchAlunoData]);


    // --- Handlers de Input com Máscara ---
    const handleCpfChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value
          .replace(/\D/g, '')
          .replace(/(\d{3})(\d)/, '$1.$2')
          .replace(/(\d{3})(\d)/, '$1.$2')
          .replace(/(\d{3})(\d{1,2})$/, '$1-$2')
          .slice(0, 14);
        setCpf(value);
    };

    const handleTelefoneChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value
          .replace(/\D/g, '')
          .replace(/^(\d{2})(\d)/, '($1) $2')
          .replace(/(\d{5})(\d)/, '$1-$2')
          .slice(0, 15);
        setTelefoneResponsavel(value);
    };

    // --- Ação de Salvar ---
    const handleSave = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!alunoId) {
            setError("Não é possível salvar sem um ID de aluno.");
            return;
        }

        setIsSaving(true);
        setError(null);
        setMessage(null);

        // Monta o payload para a API, convertendo os tipos de dados
        const payload = {
            nome,
            cpf: cpf.replace(/\D/g, ''),
            data_nascimento: data,
            sexo,
            nacionalidade,
            nome_responsavel: nomeResponsavel,
            numero_responsavel: telefoneResponsavel.replace(/\D/g, ''),
            id_turma: idTurma ? parseInt(idTurma) : null,
            faltas: faltas ? parseInt(faltas) : 0,
            etnia: etnia ? parseInt(etnia) : null,
            educacaoPais: educacaoPais ? parseInt(educacaoPais) : null,
            tempoEstudoSemanal: tempoEstudoSemanal ? parseFloat(tempoEstudoSemanal) : null,
            apoioPais: apoioPais ? 1 : 0,
            aulasParticulares: aulasParticulares ? 1 : 0,
            extraCurriculares: extraCurriculares ? 1 : 0,
            esportes: esportes ? 1 : 0,
            aulaMusica: aulaMusica ? 1 : 0,
            voluntariado: voluntariado ? 1 : 0,
        };

        try {
            const response = await fetch(`http://localhost:5000/aluno/${alunoId}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            });

            const result = await response.json();
            if (!response.ok) throw new Error(result.mensagem || "Falha ao atualizar o aluno.");
            setMessage("Aluno atualizado com sucesso!");
        } catch (err: any) {
            setError(err.message);
        } finally {
            setIsSaving(false);
        }
    };

    // --- Componente de Checkbox Reutilizável ---
    const BooleanCheckbox = ({ label, checked, onChange }: { label: string, checked: boolean, onChange: (e: React.ChangeEvent<HTMLInputElement>) => void }) => (
        <label className="flex items-center bg-[#A7C1A8] px-3 py-2 rounded-lg shadow-sm cursor-pointer hover:bg-[#8FAE91] transition-colors">
            <input type="checkbox" checked={checked} onChange={onChange} className="mr-2 accent-[#EEA03D] w-5 h-5"/>
            <span>{label}</span>
        </label>
    );
        
    return (
        <>
            <header className="font-[InknutAntiqua] bg-[#727D73] border-[#A4B465] text-[#EEA03D] border-7 h-21 text-center text-7xl fixed top-0 left-0 w-full z-50">
                IMD-IA
            </header>

            <main className="bg-[#F5ECD5] bg-[url('/imagem/backgroundloginimage.png')] bg-cover bg-center bg-no-repeat flex justify-center items-center min-h-screen py-32">
                <div className="font-[Jomolhari] bg-[#F5ECD5] border-[#A7C1A8] w-[90%] max-w-6xl p-8 rounded-3xl shadow-[0_19px_4px_4px_rgba(0,0,0,0.25)] flex flex-col gap-6 border-11">
                    <h1 className="text-[#EEA03D] text-5xl text-center">Editar Cadastro do Aluno</h1>
                    
                    {loading && <p className="text-center text-lg">Carregando dados do aluno... ⏳</p>}
                    {error && <p className="text-red-600 bg-red-100 p-3 rounded-md text-center font-semibold -my-2">{error}</p>}
                    {message && <p className="text-green-700 bg-green-100 p-3 rounded-md text-center font-semibold -my-2">{message}</p>}

                    {!loading && (
                        <form className="flex flex-col gap-8" onSubmit={handleSave}>
                            {/* Seção de Dados Pessoais e Responsável */}
                            <fieldset className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-4">
                                <div>
                                    <h5>Nome Completo</h5>
                                    <input className="w-full h-10 bg-[#A7C1A8] rounded px-3" type="text" value={nome} onChange={e => setNome(e.target.value)} required />
                                </div>
                                <div>
                                    <h5>Nome do Responsável</h5>
                                    <input className="w-full h-10 bg-[#A7C1A8] rounded px-3" type="text" value={nomeResponsavel} onChange={e => setNomeResponsavel(e.target.value)} required />
                                </div>
                                <div>
                                    <h5>Data de Nascimento</h5>
                                    <input className="w-full h-10 bg-[#A7C1A8] rounded px-3" type="date" value={data} onChange={e => setData(e.target.value)} required />
                                </div>
                                <div>
                                    <h5>Telefone do Responsável</h5>
                                    <input className="w-full h-10 bg-[#A7C1A8] rounded px-3" type="tel" value={telefoneResponsavel} onChange={handleTelefoneChange} placeholder="(XX) XXXXX-XXXX" required />
                                </div>
                                <div>
                                    <h5>CPF</h5>
                                    <input className="w-full h-10 bg-[#A7C1A8] rounded px-3" type="text" value={cpf} onChange={handleCpfChange} placeholder="000.000.000-00" required />
                                </div>
                                <div>
                                    <h5>Nacionalidade</h5>
                                    <input className="w-full h-10 bg-[#A7C1A8] rounded px-3" type="text" value={nacionalidade} onChange={e => setNacionalidade(e.target.value)} required />
                                </div>
                                <div>
                                    <h5>Gênero</h5>
                                    <select value={sexo} onChange={e => setSexo(e.target.value)} className="w-full h-10 bg-[#A7C1A8] rounded px-3" required>
                                        <option value="">Selecione...</option>
                                        <option value="Masculino">Masculino</option>
                                        <option value="Feminino">Feminino</option>
                                        <option value="Outro">Outro</option>
                                    </select>
                                </div>
                                 <div>
                                    <h5>Etnia</h5>
                                    <select value={etnia} onChange={e => setEtnia(e.target.value)} className="w-full h-10 bg-[#A7C1A8] rounded px-3">
                                        <option value="">Selecione...</option>
                                        {etniaOptions.map(opt => <option key={opt.value} value={opt.value}>{opt.label}</option>)}
                                    </select>
                                </div>
                            </fieldset>

                             {/* Seção de Dados Acadêmicos */}
                             <fieldset className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-x-12 gap-y-4">
                                <div>
                                    <h5>Turma</h5>
                                    <select value={idTurma} onChange={e => setIdTurma(e.target.value)} className="w-full h-10 bg-[#A7C1A8] rounded px-3">
                                        <option value="">Nenhuma turma</option>
                                        {turmas.map(t => <option key={t.id} value={t.id}>{t.nome}</option>)}
                                    </select>
                                </div>
                                <div>
                                    <h5>Total de Faltas</h5>
                                    <input className="w-full h-10 bg-[#A7C1A8] rounded px-3" type="number" min="0" value={faltas} onChange={e => setFaltas(e.target.value)} />
                                </div>
                                <div>
                                    <h5>Escolaridade dos Pais</h5>
                                     <select value={educacaoPais} onChange={e => setEducacaoPais(e.target.value)} className="w-full h-10 bg-[#A7C1A8] rounded px-3">
                                        <option value="">Selecione...</option>
                                        {educacaoPaisOptions.map(opt => <option key={opt.value} value={opt.value}>{opt.label}</option>)}
                                    </select>
                                </div>
                                <div>
                                    <h5>Estudo Semanal (horas)</h5>
                                    <input className="w-full h-10 bg-[#A7C1A8] rounded px-3" type="number" min="0" step="0.5" value={tempoEstudoSemanal} onChange={e => setTempoEstudoSemanal(e.target.value)} placeholder="Ex: 3.5" />
                                </div>
                            </fieldset>

                            {/* Seção de Atividades e Apoio */}
                            <fieldset className="border-t-2 border-[#A7C1A8] pt-6">
                                <legend className="text-xl text-[#727D73] px-2 -translate-y-9 bg-[#F5ECD5]">Atividades e Apoio</legend>
                                <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
                                   <BooleanCheckbox label="Apoio dos Pais" checked={apoioPais} onChange={e => setApoioPais(e.target.checked)} />
                                   <BooleanCheckbox label="Aulas Particulares" checked={aulasParticulares} onChange={e => setAulasParticulares(e.target.checked)} />
                                   <BooleanCheckbox label="Ativ. Extracurriculares" checked={extraCurriculares} onChange={e => setExtraCurriculares(e.target.checked)} />
                                   <BooleanCheckbox label="Pratica Esportes" checked={esportes} onChange={e => setEsportes(e.target.checked)} />
                                   <BooleanCheckbox label="Aulas de Música" checked={aulaMusica} onChange={e => setAulaMusica(e.target.checked)} />
                                   <BooleanCheckbox label="Faz Voluntariado" checked={voluntariado} onChange={e => setVoluntariado(e.target.checked)} />
                                </div>
                            </fieldset>
                            
                            {/* Botões de Ação */}
                            <div className="flex flex-col sm:flex-row items-center justify-center gap-6 mt-4">
                                <Link className="w-full sm:w-44 h-13 border-5 rounded-lg border-[#727D73] flex justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-2xl order-2 sm:order-1" href={"/ListaAlunos"}>
                                    Voltar
                                </Link>
                                <button type="submit" disabled={isSaving || loading} className="w-full sm:w-100 h-19 border-5 rounded-lg border-[#727D73] flex justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-4xl disabled:bg-gray-400 disabled:cursor-not-allowed disabled:text-gray-600 order-1 sm:order-2">
                                    {isSaving ? "Salvando..." : "Salvar Alterações"}
                                </button>
                            </div>
                        </form>
                    )}
                </div>
            </main>
        </>
    );
}