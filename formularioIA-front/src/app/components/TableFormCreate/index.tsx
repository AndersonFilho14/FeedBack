"use client"

import desempenho from "@/app/api/desempenho";
import { useRouter, usePathname } from "next/navigation";
import React, { useState } from "react";

const levelFeedback = [
  { value: 0, label: "Nenhum" },
  { value: 1, label: "Baixo" },
  { value: 2, label: "Moderado" },
  { value: 3, label: "Alto" },
  { value: 4, label: "Muito Alto" },
];

const radioTrueorFalseOption = [
  { value: 1, label: "Sim" },
  { value: 0, label: "Não" },
];

const askWithTrueOrFalse = [
  { name: "aulasParticulares", label: "Aulas Particulares" },
  { name: "extraCurriculares", label: "Extras Curriculares" },
  { name: "esportes", label: "Esportes" },
  { name: "aulaMusica", label: "Músicas" },
  { name: "voluntariado", label: "Voluntariado" },
];

interface FormData {
  [key: string]: string | number;
  nome: string;
  idade: number;
  sexo: number;
  etnia: number;
  educacaoPais: number;
  tempoEstudoSemanal: number;
  faltas: number;
  apoioPais: number;
  aulasParticulares: number;
  extraCurriculares: number;
  esportes: number;
  aulaMusica: number;
  voluntariado: number;
}

export default function AlunoForm() {
  const router = useRouter();
  const [formData, setFormData] = useState<FormData>({
    nome: "",
    idade: 0,
    sexo: 0,
    etnia: 0,
    educacaoPais: 0,
    tempoEstudoSemanal: 0,
    faltas: 0,
    apoioPais: 0,
    aulasParticulares: 0,
    extraCurriculares: 0,
    esportes: 0,
    aulaMusica: 0,
    voluntariado: 0,
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleRadioChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: Number(value),
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log(formData);
    await desempenho.criar(formData);
    router.push("/desempenho");
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="max-w-3xl mx-auto p-6 bg-white shadow-md rounded-lg space-y-6"
    >
      <h2 className="text-2xl font-bold mb-4">Cadastro de Aluno</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label htmlFor="nome" className="block font-medium mb-1">Nome</label>
          <input
            id="nome"
            type="text"
            name="nome"
            value={formData.nome}
            onChange={handleChange}
            placeholder="Nome"
            className="p-2 border rounded w-full"
          />
        </div>

        <div>
          <label htmlFor="idade" className="block font-medium mb-1">Idade</label>
          <input
            id="idade"
            type="number"
            name="idade"
            value={formData.idade}
            onChange={handleChange}
            placeholder="Idade"
            className="p-2 border rounded w-full"
          />
        </div>

        <div>
          <label htmlFor="sexo" className="block font-medium mb-1">Sexo</label>
          <select
            id="sexo"
            name="sexo"
            value={formData.sexo}
            onChange={handleChange}
            className="p-2 border rounded w-full"
          >
            <option value="">Selecione</option>
            <option value={0}>Masculino</option>
            <option value={1}>Feminino</option>
            <option value={2}>Outro</option>
          </select>
        </div>

        <div>
          <label htmlFor="etnia" className="block font-medium mb-1">Etnia</label>
          <select
            id="etnia"
            name="etnia"
            value={formData.etnia}
            onChange={handleChange}
            className="p-2 border rounded w-full"
          >
            <option value="">Selecione</option>
            <option value={0}>Branca</option>
            <option value={1}>Preta</option>
            <option value={2}>Parda</option>
            <option value={3}>Amarela</option>
            <option value={4}>Indígena</option>
            <option value={5}>Outra</option>
          </select>
        </div>

        <div>
          <label htmlFor="educacaoPais" className="block font-medium mb-1">Educação dos Pais</label>
          <select
            id="educacaoPais"
            name="educacaoPais"
            value={formData.educacaoPais}
            onChange={handleChange}
            className="p-2 border rounded w-full"
          >
            <option value="">Selecione</option>
            <option value={0}>Nenhuma</option>
            <option value={1}>Fundamental</option>
            <option value={2}>Médio</option>
            <option value={3}>Superior</option>
          </select>
        </div>

        <div>
          <label htmlFor="tempoEstudoSemanal" className="block font-medium mb-1">Tempo de Estudo Semanal (horas)</label>
          <input
            id="tempoEstudoSemanal"
            type="number"
            name="tempoEstudoSemanal"
            value={formData.tempoEstudoSemanal}
            onChange={handleChange}
            placeholder="Tempo de Estudo Semanal (horas)"
            className="p-2 border rounded w-full"
          />
        </div>

        <div>
          <label htmlFor="faltas" className="block font-medium mb-1">Número de Faltas</label>
          <input
            id="faltas"
            type="number"
            name="faltas"
            value={formData.faltas}
            onChange={handleChange}
            placeholder="Número de Faltas"
            className="p-2 border rounded w-full"
          />
        </div>

        <div>
          <label htmlFor="apoioPais" className="block font-medium mb-1">Apoio dos Pais</label>
          <select
            id="apoioPais"
            name="apoioPais"
            value={formData.apoioPais}
            onChange={handleChange}
            className="p-2 border rounded w-full"
          >
            <option value="">Selecione</option>
            {levelFeedback.map((level) => (
              <option key={level.value} value={level.value}>
                {level.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {askWithTrueOrFalse.map((field) => (
          <div key={field.name}>
            <label className="block font-medium mb-1">{field.label}</label>
            <div className="flex gap-4">
              {radioTrueorFalseOption.map((opt) => (
                <label key={opt.value} className="flex items-center gap-2">
                  <input
                    type="radio"
                    name={field.name}
                    value={opt.value}
                    checked={formData[field.name] === opt.value}
                    onChange={handleRadioChange}
                    className="accent-blue-600"
                  />
                  {opt.label}
                </label>
              ))}
            </div>
          </div>
        ))}
      </div>

      <button
        type="submit"
        className="bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
      >
        Enviar
      </button>
    </form>
  );
}
