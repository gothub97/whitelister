from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import TokenComplianceProfile, ContractAnalysisResult, HolderAnalysisResult
from .serializers import TokenComplianceProfileSerializer, HolderAnalysisResultSerializer
from .utils.contract import fetch_token_metadata
from .utils.contract_analysis import run_contract_analysis
from .utils.contract import get_bytecode_for_address
from .utils.holder_analysis import analyze_token_holders

import hashlib


class TokenProfileView(APIView):
    def get(self, request, address):
        address = address.lower()
        profile = TokenComplianceProfile.objects.filter(token_address__iexact=address).first()
        if profile:
            serializer = TokenComplianceProfileSerializer(profile)
            return Response(serializer.data)
        return Response({"error": "Token not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, address):
        address = address.lower()

        # Skip if already exists
        existing = TokenComplianceProfile.objects.filter(token_address__iexact=address).first()
        if existing:
            serializer = TokenComplianceProfileSerializer(existing)
            return Response(serializer.data)

        try:
            meta = fetch_token_metadata(address)
        except Exception as e:
            return Response({"error": f"Unable to fetch token metadata: {str(e)}"}, status=400)

        profile = TokenComplianceProfile.objects.create(
            token_address=address,
            name=meta["name"],
            symbol=meta["symbol"],
            decimals=meta["decimals"],
            risk_score=0.0,
            recommendation="pending",
            flags=[],
            modules={}
        )

        serializer = TokenComplianceProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TokenListView(APIView):
    def get(self, request):
        tokens = TokenComplianceProfile.objects.all().order_by("-created_at")
        data = [
            {
                "id": str(t.id),
                "token_address": t.token_address,
                "name": t.name,
                "symbol": t.symbol,
                "risk_score": t.risk_score,
                "recommendation": t.recommendation,
                "created_at": t.created_at.isoformat()
            }
            for t in tokens
        ]
        return Response({"tokens": data}, status=200)

class ContractAnalysisView(APIView):
    def post(self, request, token_id):
        try:
            token = TokenComplianceProfile.objects.get(id=token_id)
        except TokenComplianceProfile.DoesNotExist:
            return Response({"error": "Token not found"}, status=404)

        # Get raw bytecode
        try:
            bytecode = get_bytecode_for_address(token.token_address)
        except Exception as e:
            return Response({"error": f"Unable to fetch bytecode: {str(e)}"}, status=500)

        # Compute bytecode hash
        bytecode_hash = hashlib.md5(bytecode.encode()).hexdigest()

        # Run analysis on bytecode
        try:
            result = run_contract_analysis(token.token_address)
        except Exception as e:
            return Response({"error": f"Contract analysis failed: {str(e)}"}, status=500)

        # Store new analysis record
        ContractAnalysisResult.objects.create(
            token=token,
            score=result["score"],
            flags=result["flags"],
            evidence=result["evidence"],
            bytecode=bytecode,
            bytecode_hash=bytecode_hash,
            engine_version="0.1-beta"
        )

        # Update token profile with summary
        token.risk_score = result["score"]
        token.flags = result["flags"]
        token.recommendation = "enhanced_due_diligence" if result["score"] < 70 else "go"
        token.modules["contractAnalysis"] = result
        token.save()

        return Response({
            "message": "Contract analysis completed",
            "contractAnalysis": result
        }, status=200)

class ContractAnalysisListView(APIView):
    def get(self, request, token_id):
        try:
            token = TokenComplianceProfile.objects.get(id=token_id)
        except TokenComplianceProfile.DoesNotExist:
            return Response({"error": "Token not found"}, status=404)

        analyses = ContractAnalysisResult.objects.filter(token=token).order_by("-analyzed_at")
        data = [
            {
                "id": str(a.id),
                "score": a.score,
                "flags": a.flags,
                "evidence": a.evidence,
                "bytecode_hash": a.bytecode_hash,
                "engine_version": a.engine_version,
                "analyzed_at": a.analyzed_at.isoformat()
            }
            for a in analyses
        ]

        return Response({"token": str(token.id), "analyses": data}, status=200)

class HolderAnalysisView(APIView):
    def post(self, request, token_id):
        try:
            token = TokenComplianceProfile.objects.get(id=token_id)
        except TokenComplianceProfile.DoesNotExist:
            return Response({"error": "Token not found"}, status=404)

        try:
            result = analyze_token_holders(token.token_address)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

        analysis = HolderAnalysisResult.objects.create(
            token=token,
            top_holders=result["top_holders"],
            centralization_score=result["centralization_score"],
            anomalies=result["anomalies"]
        )

        token.modules["holderAnalysis"] = result
        token.save()

        serializer = HolderAnalysisResultSerializer(analysis)
        return Response(serializer.data, status=201)

    def get(self, request, token_id):
        try:
            token = TokenComplianceProfile.objects.get(id=token_id)
        except TokenComplianceProfile.DoesNotExist:
            return Response({"error": "Token not found"}, status=404)

        analyses = HolderAnalysisResult.objects.filter(token=token).order_by("-created_at")
        serializer = HolderAnalysisResultSerializer(analyses, many=True)
        return Response(serializer.data)