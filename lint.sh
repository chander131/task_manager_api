#!/bin/bash

echo "🔍 Ejecutando isort (ordenar imports)..."
isort .

echo "🎨 Ejecutando black (formatear código)..."
black .

echo "🧼 Ejecutando flake8 (linting estático)..."
flake8 .

echo "✅ Linting y formateo completados correctamente."
