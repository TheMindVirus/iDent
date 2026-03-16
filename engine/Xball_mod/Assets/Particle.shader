Shader "Custom/Particle"
{
    Properties
    {
        _Chroma ("Chroma", Color) = (1, 1, 1, 1.0)
        _Texture ("Texture", 2D) = "" {}
        _Metallic ("Metallic", Range(0, 1)) = 1.0
        _Smoothness ("Smoothness", Range(0, 1)) = 1.0
    }
    SubShader
    {
        Tags { "RenderType" = "Opaque" "Queue" = "Geometry" }

        CGPROGRAM
        #pragma target 3.0
        #pragma surface surface Standard fullforwardshadows

        fixed4 _Chroma;
        sampler2D _Texture;
        fixed _Metallic;
        fixed _Smoothness;

        struct Input
        {
            fixed2 uv_Texture;
        };

        void surface(Input IN, inout SurfaceOutputStandard output)
        {
            fixed4 c = tex2D(_Texture, IN.uv_Texture) * _Chroma;
            output.Albedo = c.rgb;
            output.Alpha = c.a;
            output.Metallic = _Metallic;
            output.Smoothness = _Smoothness;
        }
        ENDCG
    }
}
