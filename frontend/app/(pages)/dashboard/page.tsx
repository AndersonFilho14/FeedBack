"use client";
import AveragePerClass from "@/components/AvaragePerClass";
import AveragePerSchool from "@/components/AveragePerSchool";
import BestStudentTable from "@/components/BestStudentTable";
import AverageTeacher from "@/components/AverageTeacher";
import React from "react";
import DistributionSchoolIA from "@/components/DistributionSchoolIA";
import DistSchoolAIMale from "@/components/DistSchoolAIMale";
import DistSchoolAIFemale from "@/components/DistSchoolAIFemale";
import { Button, Card, Typography } from "antd";
import { gerarPDF } from "@/utils/gerarPDF";

function DashboardPage() {
  const { Title } = Typography;

  return (
    <>
      <header className="font-[InknutAntiqua] bg-[#727D73] border-[#A4B465] text-[#EEA03D] border-7 h-21 text-center text-7xl fixed top-0 left-0 w-full z-40">
        IMD-IA
      </header>

      <div className="bg-[#F5ECD5]  bg-cover bg-center bg-no-repeat min-h-screen w-full  pt-28 pb-50 px-4 sm:px-8">
        <main className="max-w-7xl mx-auto">
          <h1 className="font-[Jomolhari] text-5xl text-[#EEA03D] text-center mb-10">
            Dashboard do Município
          </h1>
          <div className="flex w-full justify-end">
            <Button
              size="large"
              type="primary"
              className="mb-6"
              onClick={() => {
                gerarPDF(document.getElementById("relatorio-completo"));
              }}
            >
              Baixar PDF
            </Button>
          </div>
          {/* Grid para os componentes do dashboard com espaçamento */}
          <div id="relatorio-completo">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
              <BestStudentTable hidePageButtons />
              <AveragePerClass />
              <AveragePerSchool />
              <AverageTeacher />
            </div>
            <Card style={{ marginTop: 180 }}>
              <Title level={3}>IA</Title>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
                <DistributionSchoolIA />
                <DistSchoolAIMale />
                <DistSchoolAIFemale />
              </div>
            </Card>
          </div>
        </main>
      </div>
    </>
  );
}

export default DashboardPage;
