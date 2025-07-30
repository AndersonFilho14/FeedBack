// /app/dashboardPdf/page.tsx
"use client";

import React from "react";
import html2canvas from "html2canvas";
import jsPDF from "jspdf";
import DistributionSchoolIA from "@/components/DistributionSchoolIA";
import DistSchoolAIFemale from "@/components/DistSchoolAIFemale";
import DistSchoolAIMale from "@/components/DistSchoolAIMale";
import AveragePerSchool from "@/components/AveragePerSchool";
import BestStudentTable from "@/components/BestStudentTable";
import AverageTeacher from "@/components/AverageTeacher";
import AveragePerClass from "@/components/AveragePerSchool";

import { Card, Typography } from "antd";

export default function DashboardPdfPage() {
  const gerarPDF = async () => {
    const elemento = document.getElementById("relatorio-completo");
    if (!elemento) return;

    const canvas = await html2canvas(elemento, {
      scale: 2,
      useCORS: true,
    });

    const imgData = canvas.toDataURL("image/png");
    const pdf = new jsPDF("p", "mm", "a4");

    const imgProps = pdf.getImageProperties(imgData);
    const pdfWidth = pdf.internal.pageSize.getWidth();
    const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;

    pdf.addImage(imgData, "PNG", 0, 0, pdfWidth, pdfHeight);
    pdf.save("relatorio-desempenho.pdf");
  };

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <button
        className="mb-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        onClick={gerarPDF}
      >
        Baixar Relatório em PDF
      </button>

      <div
        id="relatorio-completo"
        className="bg-white p-6 rounded shadow space-y-4"
      >
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
          <BestStudentTable hidePageButtons={true} />
          <AveragePerClass />
          <AveragePerSchool />
          <AverageTeacher />
        </div>
        <Card style={{ marginTop: 16 }}>
          <Typography.Title level={3}>IA</Typography.Title>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
            <DistributionSchoolIA />
            <DistSchoolAIMale />
            <DistSchoolAIFemale />
          </div>
        </Card>
      </div>
    </div>
  );
}
